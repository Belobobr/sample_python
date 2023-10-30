// api
interface Cloud {
  cloud_name: string;
  geo_region: string;
  cloud_description?: string;
  geo_latitude?: number;
  geo_longitude?: number;
  provider?: string;
  provider_description?: string;
}

// class CloudFilter {
//   constructor(public provider?: string) {}
// }

interface CloudFilter {
  provider?: string;
}

// class CloudSort {
//   constructor(public user_geo_latitude: number, public user_geo_longitude: number) {}
// }

interface CloudSort {
  user_geo_latitude?: number;
  user_geo_longitude?: number;
}

export type { Cloud, CloudFilter, CloudSort };

// export type { Cloud };

// export { CloudFilter, CloudSort }
