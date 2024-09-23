from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    App,
    Stack,
)
from constructs import Construct

class ApiGatewayStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_handler_arn = self.node.try_get_context("lambda_handler_arn")
        lambda_name = self.node.try_get_context("lambda_name")

        lambda_function = _lambda.Function.from_function_arn(self, lambda_name, lambda_handler_arn)

        api = apigateway.RestApi(self, "ApiGateway",
                                 rest_api_name="ApiGatewayName",
                                 default_cors_preflight_options={
                                     "allow_origins": apigateway.Cors.ALL_ORIGINS,
                                     "allow_methods": apigateway.Cors.ALL_METHODS,
                                 })

        name_resource = api.root.add_resource("name")

        post_integration = apigateway.LambdaIntegration(
            handler=lambda_function,
            proxy=True
        )

        name_resource.add_method("POST", post_integration)

app = App()
ApiGatewayStack(app, "ApiGatewayStack")
app.synth()
