from aws_cdk import (
    aws_apigateway as apigateway,
    core
)

class ApiGatewayStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        api = apigateway.RestApi(self, "ApiGateway",
                                 rest_api_name="ApiGatewayName",
                                 default_cors_preflight_options={
                                     "allow_origins": apigateway.Cors.ALL_ORIGINS,
                                     "allow_methods": apigateway.Cors.ALL_METHODS,
                                 })

        name_resource = api.root.add_resource("name")

        mock_integration = apigateway.MockIntegration(
            integration_responses=[{
                'statusCode': '200',
                'responseTemplates': {
                    'application/json': '{"message": "This is a mock response!"}'
                }
            }],
            request_templates={
                'application/json': '{"statusCode": 200}'
            }
        )

        name_resource.add_method("POST", mock_integration,
                                 method_responses=[{
                                     'statusCode': '200',
                                     'responseModels': {
                                         'application/json': apigateway.Model.EMPTY_MODEL
                                     }
                                 }])

