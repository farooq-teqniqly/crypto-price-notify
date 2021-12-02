targetScope = 'subscription'

param solutionName string

@allowed([
  'dev'
  'prod'
])
param environmentName string

param appSettings object

var location = deployment().location
var baseName = '${solutionName}-${environmentName}-${location}'
var rgName = '${baseName}-rg'

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: rgName
  location: location
}

module eventHubDeploy 'EventHub.bicep' = {
  name: 'eventHubDeploy'
  scope: rg
  params: {
    baseName: baseName
    location: location
  }
}

module resourcesDeploy 'FunctionApp.bicep' = {
  name: 'resourcesDeploy'
  scope: rg
  params: {
     appSettings: appSettings
     baseName: baseName
     location: location 
     eventHubConnectionString: eventHubDeploy.outputs.deploymentOutputs.eventHub.connectionString
  }
}

output deploymentOutputs object = {
  resourceGroupName: rgName
  eventHubDeployment: {
    connectionString: eventHubDeploy.outputs.deploymentOutputs.eventHub.connectionString
    name: eventHubDeploy.outputs.deploymentOutputs.eventHub.name
  }
}
