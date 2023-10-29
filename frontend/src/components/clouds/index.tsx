// FilterableAndSortableCloudTable
// CloudFilter / CloudSort
// CloudTable
// CloudRow

import { Cloud } from '../../entities';

function CloudRow({ cloud }: { cloud: Cloud }) {
  // const name = product.stocked ? product.name :
  //   <span style={{ color: 'red' }}>
  //     {product.name}
  //   </span>;

  const { cloud_name, geo_region, cloud_description, geo_latitude, geo_longitude, provider, provider_description } =
    cloud;

  return (
    <tr>
      <td>{cloud_name}</td>
      <td>{geo_region}</td>
      <td>{cloud_description}</td>
      <td>{geo_latitude}</td>
      <td>{geo_longitude}</td>
      <td>{provider}</td>
      <td>{provider_description}</td>
    </tr>
  );
}

export { CloudRow };
