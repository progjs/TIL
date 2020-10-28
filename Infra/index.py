import json
import boto3

sns = boto3.client('sns')
code_pipeline = boto3.client('codepipeline')

# 메인 함수
def lambda_handler(event, context):
    
    def get_user_params(pipeline_data):
    decoded_parameters = ''
    try:
        user_parameters = pipeline_data['data']['actionConfiguration']['configuration']['UserParameters']
        decoded_parameters = json.loads(user_parameters)
    except Exception:
        decoded_parameters = ''
        # raise Exception('UserParameters could not be decoded as JSON')
    return decoded_parameters

    print('EVENT--------')
    print(event)
    jobId = event['CodePipeline.job']['id']

    snsParams = {
        'Message': '{} 배포 완료!'.format(get_user_params(event['CodePipeline.job'])),
        'TopicArn': 'arn:aws:sns:ap-northeast-2:013223759423:code-pipline-notification'
    }
    try:
        sns.publish(snsParams)
    except Exception as snsErr:
        print(snsErr)
        pipelineParams = {
            'jobId': jobId,
            'failureDetails': {
                'message': json.dumps(snsErr), 
                'type': 'JobFailed',
                'externalExecutionId': context['invokeid']
            }
        }

        try:
            code_pipeline.put_job_failure_result(pipelineParams)
        except Exception as pipelineErr:
            print(pipelineErr)
            print('SNS: success, CodePipeline: fail')
            return pipelineErr
    # sns 성공
    try:
        code_pipeline.put_job_success_result(jobId=jobId)
    except Exception as pipelineErr:
        print(pipelineErr)
        print('SNS: success, CodePipeline: fail')
        return pipelineErr
    return 

    