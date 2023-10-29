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

// export {
//     Cloud,
// }

export type { Cloud };
