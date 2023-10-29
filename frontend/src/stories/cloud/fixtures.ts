const azureCloudAllFields = {
  cloud_description: 'Azure',
  cloud_name: 'azure-south-africa-north',
  geo_latitude: -25,
  geo_longitude: 28,
  geo_region: 'africa',
  provider: 'azure',
  provider_description: 'Microsoft Azure',
};

const azureCloudRequiredFields = {
  cloud_name: 'azure-south-africa-north',
  geo_region: 'africa',
};

const cloudsAllFields = [
  {
    cloud_description: 'Azure',
    cloud_name: 'azure-south-africa-north',
    geo_latitude: -25,
    geo_longitude: 28,
    geo_region: 'africa',
    provider: 'azure',
    provider_description: 'Microsoft Azure',
  },
  {
    cloud_description: 'Asia, Singapore - UpCloud: Singapore',
    cloud_name: 'upcloud-sg-sin',
    geo_latitude: 1,
    geo_longitude: 103,
    geo_region: 'asia-pacific',
    provider: 'upcloud',
    provider_description: 'UpCloud',
  },
  {
    cloud_description: 'Asia, Hong Kong - Google Cloud: Hong Kong',
    cloud_name: 'google-asia-east2',
    geo_latitude: 22,
    geo_longitude: 114,
    geo_region: 'asia-pacific',
    provider: 'google',
    provider_description: 'Google Cloud Platform',
  },
  {
    cloud_description: 'Asia, India - DigitalOcean: Bangalore',
    cloud_name: 'do-blr',
    geo_latitude: 12,
    geo_longitude: 77,
    geo_region: 'asia-pacific',
    provider: 'do',
    provider_description: 'DigitalOcean',
  },
  {
    cloud_description: 'Africa, South Africa - Amazon Web Services: Cape Town',
    cloud_name: 'aws-af-south-1',
    geo_latitude: -33,
    geo_longitude: 18,
    geo_region: 'africa',
    provider: 'aws',
    provider_description: 'Amazon Web Services',
  },
];

const cloudRequiredFields = [
  {
    cloud_name: 'azure-south-africa-north',
    geo_region: 'africa',
  },
  {
    cloud_name: 'upcloud-sg-sin',
    geo_region: 'asia-pacific',
  },
  {
    cloud_name: 'google-asia-east2',
    geo_region: 'asia-pacific',
  },
  {
    cloud_name: 'do-blr',
    geo_region: 'asia-pacific',
  },
  {
    cloud_name: 'aws-af-south-1',
    geo_region: 'africa',
  },
];

export { azureCloudAllFields, azureCloudRequiredFields, cloudsAllFields, cloudRequiredFields };


