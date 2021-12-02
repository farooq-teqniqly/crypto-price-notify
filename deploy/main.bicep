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

module resourcesDeploy 'resources.bicep' = {
  name: 'resourcesDeploy'
  scope: rg
  params: {
     appSettings: appSettings
     baseName: baseName
     location: location 
  }
}
