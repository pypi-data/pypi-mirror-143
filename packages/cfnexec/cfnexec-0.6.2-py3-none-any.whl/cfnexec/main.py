"""This is a cfn-exec main program."""
import requests
import json
import os
import argparse
import re
import boto3
import logging
from pathlib import Path
import uuid
import glob
try:
    from cfnexec import version
except:
    import version
import yaml
from awscli.customizations.cloudformation.yamlhelper import yaml_parse

logger = logging.getLogger(__name__)

def isUrl(path: str):
    pattern = r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    result = ''
    if re.match(pattern, path):
        return True
    else:
        return False

def read_s3_file(url: str):
    s3 = boto3.resource('s3')
    url_sp = url.split('/')
    domain_sp = url_sp[2].split('.')
    bucket = s3.Bucket(domain_sp[0])
    obj  = bucket.Object('/'.join(url_sp[3:]))
    response = obj.get()    
    body = response['Body'].read()

    return body.decode('utf-8')

def create_s3():
    bucket_name = 'cfn-exec-' + boto3.session.Session().region_name + '-' + str(uuid.uuid4())
    logger.debug('Create s3 bucket: ' + bucket_name)
    s3 = boto3.resource('s3', region_name=boto3.session.Session().region_name)
    bucket = s3.Bucket(bucket_name)
    bucket.create(CreateBucketConfiguration={'LocationConstraint': boto3.session.Session().region_name})
    return bucket_name

def upload_file_to_s3(bucket_name: str, filepath_list: list, root_path: str):
    s3 = boto3.resource('s3', region_name=boto3.session.Session().region_name)
    root_path_str = str(Path(root_path).resolve())
    for f in filepath_list:
        logger.debug('Upload s3 bucket: ' + f)
        f_str = str(Path(f).resolve())
        s3.Object(bucket_name, f_str.replace(root_path_str, '')[1:]).upload_file(f)

def get_public_url(bucket, target_object_path):
    s3 = boto3.client('s3', region_name=boto3.session.Session().region_name)
    bucket_location = s3.get_bucket_location(Bucket=bucket)
    return "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        bucket_location['LocationConstraint'],
        bucket,
        target_object_path)

def delete_bucket(bucket_name, dryrun=False):
    contents_count = 0
    next_token = ''
    client = boto3.client('s3')

    while True:
        if next_token == '':
            response = client.list_objects_v2(Bucket=bucket_name)
        else:
            response = client.list_objects_v2(Bucket=bucket_name, ContinuationToken=next_token)

        if 'Contents' in response:
            contents = response['Contents']
            contents_count = contents_count + len(contents)
            for content in contents:
                if not dryrun:
                    logger.debug("Deleting: s3://" + bucket_name + "/" + content['Key'])
                    client.delete_object(Bucket=bucket_name, Key=content['Key'])
                else:
                    logger.debug("DryRun: s3://" + bucket_name + "/" + content['Key'])

        if 'NextContinuationToken' in response:
            next_token = response['NextContinuationToken']
        else:
            break
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.delete()


def find_cfn_files(base_folder_path: str):
    filepath_list = []
    filepath_list.extend(list(glob.glob(os.path.join(base_folder_path + "/**/*.json"), recursive=True)))
    filepath_list.extend(list(glob.glob(os.path.join(base_folder_path + "/**/*.yml"), recursive=True)))
    filepath_list.extend(list(glob.glob(os.path.join(base_folder_path + "/**/*.yaml"), recursive=True)))
    filepath_list.extend(list(glob.glob(os.path.join(base_folder_path + "/**/*.template"), recursive=True)))
    return filepath_list

def upload_cfn(input_path: str):
    
    bucket_name = create_s3()
    filepath_list = find_cfn_files(str(Path(input_path).parent))
    upload_file_to_s3(bucket_name, filepath_list, str(Path(input_path).parent))
    return get_public_url(bucket_name, Path(input_path).name), bucket_name


def load_parameter_file(param_path: str):
    root, ext = os.path.splitext(param_path)
    content = ''
    if isUrl(param_path):
        if 's3.' in param_path and '.amazonaws.com' in param_path:
            content = read_s3_file(param_path)
        else:
            res = requests.get(param_path)
            content = res.text
    else:
        with open(param_path, encoding='utf-8') as f:
            content = f.read()
    if ext == '.json':
        result = json.loads(content)
    else:
        result = yaml.safe_load(content)
    return result

def generate_parameter(param_path: str, s3_bucket_url_parameter_key_name: str, bucket_name: str):
    param = load_parameter_file(param_path)

    result = []
    if isinstance(param, list):
        if len(list(filter(lambda p: 'ParameterKey' in p and 'ParameterValue' in p, param))) == len(param):
            result = param
        else:
            raise('Not support parameter file')
    elif isinstance(param, dict):
        result = []
        for k, v in param.items():
            if isinstance(v, dict) or isinstance(v, list):
                raise('Not support parameter file')
            result.append({
                'ParameterKey': k,
                'ParameterValue': v
            })
    else:
        raise('Not support parameter file')
    if s3_bucket_url_parameter_key_name != None:
        for r in list(filter(lambda p: p['ParameterKey'] == s3_bucket_url_parameter_key_name, result)):
            r['ParameterValue'] = 'https://{}.s3.amazonaws.com'.format(bucket_name)
    return result

def create_stack(stack_name: str, cfn_url: str, param_list: list, disable_rollback: bool, role_arn: str):
    client = boto3.client('cloudformation')
    logger.info('StackName: ' + stack_name)
    logger.info('CFn URL: ' + cfn_url)
    logger.info('Parameters: ' + json.dumps(param_list))
    response = client.validate_template(
        TemplateURL=cfn_url
    )
    if role_arn != None:
        response = client.create_stack(
            StackName=stack_name,
            TemplateURL=cfn_url,
            Parameters=param_list,
            Capabilities=[
                'CAPABILITY_IAM',
                'CAPABILITY_NAMED_IAM',
                'CAPABILITY_AUTO_EXPAND'
            ],
            DisableRollback=disable_rollback,
            RoleARN=role_arn
        )
    else:
        response = client.create_stack(
            StackName=stack_name,
            TemplateURL=cfn_url,
            Parameters=param_list,
            Capabilities=[
                'CAPABILITY_IAM',
                'CAPABILITY_NAMED_IAM',
                'CAPABILITY_AUTO_EXPAND'
            ],
            DisableRollback=disable_rollback
        )
    logger.info("CFn Stack start.")
    waiter = client.get_waiter('stack_create_complete')
    waiter.wait(StackName=stack_name) # スタック完了まで待つ
    logger.info("CFn Stack end.") # スタック完了後に実行される処理
    return response

def main():
    """cfn-exec main"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input-path",
        type=str,
        action="store",
        help="Cloudformation file url path having Cloudformation files. \
            Supported yaml and json. If this path is a folder, it will be detected recursively.",
        dest="input_path"
    )
    parser.add_argument(
        "-n", "--stack-name",
        type=str,
        action="store",
        help="The name that's associated with the stack. The name must be unique in the Region in which you are creating the stack.",
        dest="stack_name"
    )
    parser.add_argument(
        "-p", "--parameter-file",
        type=str,
        action="store",
        dest="param",
        help="Parameter file"
    )
    parser.add_argument(
        "--disable-rollback",
        type=bool,
        action="store",
        default=False,
        dest="disable_rollback",
        help="Set to true to disable rollback of the stack if stack creation failed. You can specify either DisableRollback or OnFailure , but not both."
    )
    parser.add_argument(
        "--role-arn",
        type=str,
        action="store",
        dest="role_arn",
        help="The Amazon Resource Name (ARN) of an Identity and Access Management (IAM) role that CloudFormation assumes to create the stack. CloudFormation uses the role's credentials to make calls on your behalf. CloudFormation always uses this role for all future operations on the stack. Provided that users have permission to operate on the stack, CloudFormation uses this role even if the users don't have permission to pass it. Ensure that the role grants least privilege.\nIf you don't specify a value, CloudFormation uses the role that was previously associated with the stack. If no role is available, CloudFormation uses a temporary session that's generated from your user credentials."
    )
    parser.add_argument(
        "-s3", "--s3-bucket-url-parameter-key-name",
        type=str,
        action="store",
        dest="s3_bucket_url_parameter_key_name",
        help="Set the parameter key name to this, if the input path is a local file and you want to reflect the S3 bucket name to be uploaded in the parameter."
    )
    parser.add_argument(
        "-v", "--version",
        action='version',
        version=version.__version__,
        help="Show version information and quit."
    )
    parser.add_argument(
        "-V", "--verbose",
        action='store_true',
        dest="detail",
        help="give more detailed output"
    )
    args = parser.parse_args()

    if args.detail:
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        logger.info('Set detail log level.')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        
    logger.info('Start to create stack')

    bucket_name = ''
    if isUrl(args.input_path):
        cfn_url = args.input_path
    else:
        cfn_url, bucket_name = upload_cfn(args.input_path)
    try:
        param = generate_parameter(args.param, args.s3_bucket_url_parameter_key_name, bucket_name)
        stack = create_stack(args.stack_name, cfn_url, param, args.disable_rollback, args.role_arn)
    except Exception as e:
        logger.error(e)
    if isUrl(args.input_path):
        pass
    else:
        delete_bucket(bucket_name)

    logger.info('Successfully to create stack: ' + stack['StackId'])

if __name__ == "__main__":
    # execute only if run as a script
    main()
