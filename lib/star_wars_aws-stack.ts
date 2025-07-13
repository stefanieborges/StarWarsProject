import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class StarWarsAwsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

     // Cria tabela DynamoDB 'users'
    const usersTable = new dynamodb.Table(this, 'UsersTable', {
      tableName: 'users',
      partitionKey: { name: 'username', type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.RETAIN, // Só para dev/teste Destroy, em produção use RETAIN
    });

    // Lambda Docker
    const dockerFunc = new lambda.DockerImageFunction(this, 'DockerFunc', {
      code: lambda.DockerImageCode.fromImageAsset('./image'),
      memorySize: 1024,
      timeout: cdk.Duration.seconds(10),
      architecture: lambda.Architecture.X86_64,
      environment: {
        USERS_TABLE_NAME: usersTable.tableName,  // << adiciona aqui
      }
    });

    usersTable.grantReadWriteData(dockerFunc);

    // API Gateway REST
    const api = new apigateway.LambdaRestApi(this, 'StarWarsApi', {
      handler: dockerFunc,
      proxy: true,
      restApiName: 'StarWarsService',
      deployOptions: {
        stageName: 'prod',
      },
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: ['*'],
      },
      defaultMethodOptions: {
        authorizationType: apigateway.AuthorizationType.NONE,
      }
    });

    // Output da URL
    new cdk.CfnOutput(this, 'ApiGatewayUrl', {
      value: api.url,
    });
  }
}
