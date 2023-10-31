import { useState } from 'react';
import { Cloud, CloudFilter as CloudFilterEntity, CloudSort as CloudSortEntity } from '../../entities';
import { api, ApiErrors, hasApiErrors } from '../../api';

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
    <table data-testid={'searchContent'}>
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

function CloudFilter({
  filter,
  onFilterChange,
}: {
  filter: CloudFilterEntity;
  onFilterChange: (filter: CloudFilterEntity) => void;
}) {
  return (
    <>
      <label>
        Provider:
        <input
          type="text"
          placeholder=""
          value={filter.provider}
          onChange={(e) => onFilterChange({ ...filter, provider: e.target.value })}
          data-testid={'filterProviderInput'}
        />
      </label>
    </>
  );
}

function CloudSort({ sort, onSortChange }: { sort: CloudSortEntity; onSortChange: (sort: CloudSortEntity) => void }) {
  return (
    <>
      <label>
        User geo latitude:
        <input
          type="text"
          placeholder=""
          value={sort.user_geo_latitude}
          onChange={(e) => {
            onSortChange({ ...sort, user_geo_latitude: parseFloat(e.target.value) });
          }}
          data-testid={'sortUserGeoLatitudeInput'}
        />
      </label>
      <label>
        User geo longitude:
        <input
          type="text"
          placeholder=""
          value={sort.user_geo_longitude}
          onChange={(e) => {
            onSortChange({ ...sort, user_geo_longitude: parseFloat(e.target.value) });
          }}
          data-testid={'sortUserGeoLongitudeInput'}
        />
      </label>
    </>
  );
}

function CloudSortAndFilter({
  filter,
  sort,
  onFilterChange,
  onSortChange,
  onSearchPress,
}: {
  filter: CloudFilterEntity;
  sort: CloudSortEntity;
  onSortChange: (sort: CloudSortEntity) => void;
  onFilterChange: (filter: CloudFilterEntity) => void;
  onSearchPress: () => void;
}) {
  return (
    <form
      onSubmit={(e: React.SyntheticEvent) => {
        e.preventDefault();
        onSearchPress();
      }}
    >
      <div>
        Filter:
        <div>
          <CloudFilter filter={filter} onFilterChange={onFilterChange} />
        </div>
      </div>
      <div>
        Sort:
        <div>
          <CloudSort sort={sort} onSortChange={onSortChange} />
        </div>
      </div>
      <input type="submit" value="Search" data-testid={'searchButton'} />
    </form>
  );
}

function Loader() {
  return <div data-testid={'searchLoader'}>Loading...</div>;
}

function Errors({ errors }: { errors: ApiErrors }) {
  return <div data-testid={'searchError'}>Errors: {JSON.stringify(errors)}</div>;
}

function FilterableAndSortableCloudTable({
  clouds,
  filter,
  sort,
  onFilterChange,
  onSortChange,
  onSearchPress,
  loading,
  errors,
}: {
  clouds: Cloud[];
  filter: CloudFilterEntity;
  sort: CloudSortEntity;
  onSortChange: (sort: CloudSortEntity) => void;
  onFilterChange: (filter: CloudFilterEntity) => void;
  onSearchPress: () => void;
  loading: boolean;
  errors: ApiErrors;
}) {
  let content = null;
  if (loading) {
    content = <Loader />;
  } else if (hasApiErrors(errors)) {
    content = <Errors errors={errors} />;
  } else {
    content = <CloudsTable clouds={clouds} />;
  }

  return (
    <div>
      <CloudSortAndFilter
        filter={filter}
        sort={sort}
        onFilterChange={onFilterChange}
        onSortChange={onSortChange}
        onSearchPress={onSearchPress}
      />
      {content}
    </div>
  );
}

function FilterableAndSortableCloudTableContainer() {
  const [filter, setFilter] = useState<CloudFilterEntity>({
    provider: '',
  });
  const [sort, setSort] = useState<CloudSortEntity>({
    // user_geo_latitude: 0,
    // user_geo_longitude: 0,
  });

  //TODO useReducer if it's easier to understand
  const [loading, setLoading] = useState<boolean>(false);
  const [clouds, setClouds] = useState<Cloud[]>([]);
  const [errors, setErrors] = useState<ApiErrors>({});

  const searchClouds = async () => {
    setLoading(true);
    const { errors, result: clouds } = await api.searchClouds({ filter, sort });
    setErrors(errors);
    setClouds(clouds);
    setLoading(false);
  };

  return (
    <FilterableAndSortableCloudTable
      filter={filter}
      sort={sort}
      onFilterChange={setFilter}
      onSortChange={setSort}
      onSearchPress={() => {
        void searchClouds();
      }}
      clouds={clouds}
      loading={loading}
      errors={errors}
    />
  );
}

export {
  CloudRow,
  CloudsTable,
  CloudFilter,
  CloudSort,
  FilterableAndSortableCloudTable,
  FilterableAndSortableCloudTableContainer,
  Errors,
};
