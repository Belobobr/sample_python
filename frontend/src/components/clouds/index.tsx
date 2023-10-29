// FilterableAndSortableCloudTable
// CloudFilter / CloudSort
// CloudTable
// CloudRow

import { Cloud } from '../../entities';

function CloudRow({ cloud }: { cloud: Cloud }) {
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

function CloudsTable({ clouds }: { clouds: Cloud[] }) {
  const rows = clouds.map((cloud) => <CloudRow cloud={cloud} key={cloud.cloud_name} />);

  return (
    <table>
      <thead>
        <tr>
          <th>Cloud name</th>
          <th>Geo region</th>
          <th>Cloud description</th>
          <th>Geo latitude</th>
          <th>Geo longitude</th>
          <th>Provider</th>
          <th>Provider description</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
}

function CloudFilter() {
  return (
    <form>
      <label>
        Provider:
        <input type="text" placeholder="" />
      </label>
    </form>
  );
}

function CloudSort() {
  return (
    <form>
      <label>
        User geo latitude:
        <input type="text" placeholder="" />
      </label>
      <label>
        User geo longitude:
        <input type="text" placeholder="" />
      </label>
    </form>
  );
}

function FilterableAndSortableCloudTable({ clouds }: { clouds: Cloud[] }) {
  return (
    <div>
      <CloudFilter />
      <CloudSort />
      <CloudsTable clouds={clouds} />
    </div>
  );
}

export { CloudRow, CloudsTable, CloudFilter, CloudSort, FilterableAndSortableCloudTable };
