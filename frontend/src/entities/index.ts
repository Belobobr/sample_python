interface Cloud {
  cloud_name: string;
  geo_region: string;
  cloud_description?: string;
  geo_latitude?: number;
  geo_longitude?: number;
  provider?: string;
  provider_description?: string;
}

interface CloudFilter {
  provider?: string;
}

interface CloudSort {
  user_geo_latitude?: number;
  user_geo_longitude?: number;
}

export type { Cloud, CloudFilter, CloudSort };
