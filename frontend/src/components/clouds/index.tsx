// FilterableAndSortableCloudTable
// CloudFilter / CloudSort
// CloudTable
// CloudRow

import { useState } from 'react';
import { Cloud, CloudFilter as CloudFilterEntity, CloudSort as CloudSortEntity} from '../../entities';

function CloudRow({ cloud }: { cloud: Cloud }) {
  const { cloud_name, geo_region, cloud_description, geo_latitude, geo_longitude, provider, provider_description } = cloud;

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

function CloudFilter(
  { filter, onFilterChange }: { filter: CloudFilterEntity, onFilterChange: (filter: CloudFilterEntity) => void }
) {
  return (
    <>
      <label>
        Provider:
        <input 
          type="text" 
          placeholder="" 
          value={filter.provider} 
          onChange={(e) => onFilterChange({ ...filter, provider: e.target.value })}
        />
      </label>
    </>
  );
}

function CloudSort(
  { sort, onSortChange }: { sort: CloudSortEntity, onSortChange: (sort: CloudSortEntity) => void}
) {
  return (
    <>
      <label>
        User geo latitude:
        <input 
          type="text" 
          placeholder="" 
          value={sort.user_geo_latitude}
          onChange={(e) => {
            onSortChange({...sort, user_geo_latitude: parseFloat(e.target.value)})
          }}
        />
      </label>
      <label>
        User geo longitude:
        <input 
          type="text"
          placeholder="" 
          value={sort.user_geo_longitude}
          onChange={(e) => {
            onSortChange({...sort, user_geo_longitude: parseFloat(e.target.value)})
          }}
        />
      </label>
    </>
  );
}

function CloudSortAndFilter(
  { filter, sort, onFilterChange, onSortChange }: 
  { 
    filter: CloudFilterEntity, 
    sort: CloudSortEntity, 
    onSortChange: (sort: CloudSortEntity) => void, 
    onFilterChange: (filter: CloudFilterEntity) => void 
  }
) {
  return (
    <form>
      <div>
        Filter:
        <div>
          <CloudFilter filter={filter} onFilterChange={onFilterChange}/>
        </div>
      </div>
      <div>
        Sort:
        <div>
          <CloudSort sort={sort} onSortChange={onSortChange}/>
        </div>
      </div>
      <input type="submit" value="Submit" />
    </form>
  );
}

function FilterableAndSortableCloudTable(
  { clouds, filter, sort, onFilterChange, onSortChange}: 
  { 
    clouds: Cloud[], 
    filter: CloudFilterEntity, 
    sort: CloudSortEntity, 
    onSortChange: (sort: CloudSortEntity) => void, 
    onFilterChange: (filter: CloudFilterEntity) => void  
  }
) {

  return (
    <div>
      <CloudSortAndFilter 
        filter={filter} 
        sort={sort} 
        onFilterChange={onFilterChange} 
        onSortChange={onSortChange}
      />
      <CloudsTable clouds={clouds} />
    </div>
  );
}

function FilterableAndSortableCloudTableContainer() {
  const [filter, setFilter] = useState<CloudFilterEntity>({});
  const [sort, setSort] = useState<CloudSortEntity>({});

  return (
    <FilterableAndSortableCloudTable
      clouds={[]}
      filter={filter}
      sort={sort}
      onFilterChange={setFilter}
      onSortChange={setSort}
    />
  );
}



export { CloudRow, CloudsTable, CloudFilter, CloudSort, FilterableAndSortableCloudTable };
