import { useState } from 'react';
import { Cloud, CloudFilter as CloudFilterEntity, CloudSort as CloudSortEntity } from '../../entities';
import { api, ApiErrors, hasApiErrors } from '../../api';
import { isNullOrEmpty } from '../../utils/strings';

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

function CloudSort({ sort, onSortChange }: { sort: SortForm; onSortChange: (sort: SortForm) => void }) {
  return (
    <>
      <label>
        User geo latitude:
        <input
          type="text"
          placeholder=""
          value={sort.user_geo_latitude}
          onChange={(e) => {
            onSortChange({ ...sort, user_geo_latitude: e.target.value });
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
            onSortChange({ ...sort, user_geo_longitude: e.target.value });
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
  sort: SortForm;
  onSortChange: (sort: SortForm) => void;
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
  sort: SortForm;
  onSortChange: (sort: SortForm) => void;
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

interface SortForm {
  user_geo_latitude?: string;
  user_geo_longitude?: string;
}

function parseFloatOrUndefined(str: string) {
  const value = parseFloat(str);
  return isNaN(value) ? undefined : value;
}

function getSortEntityFromSortForm(form: SortForm): CloudSortEntity | undefined {
  const user_geo_latitude = parseFloatOrUndefined(form.user_geo_latitude || '');
  const user_geo_longitude = parseFloatOrUndefined(form.user_geo_longitude || '');

  if (user_geo_latitude == undefined || user_geo_longitude == undefined) {
    return undefined;
  }

  return {
    user_geo_latitude,
    user_geo_longitude,
  };
}

// TODO
// useReducer
// use something for working with forms like formik

function FilterableAndSortableCloudTableContainer() {
  const [filter, setFilter] = useState<CloudFilterEntity>({
    provider: '',
  });
  const [sort, setSort] = useState<SortForm>({});

  const [loading, setLoading] = useState<boolean>(false);
  const [clouds, setClouds] = useState<Cloud[]>([]);
  const [errors, setErrors] = useState<ApiErrors>({});

  const searchClouds = async () => {
    setLoading(true);

    const searchFilter = isNullOrEmpty(filter.provider) ? undefined : filter;

    const { errors, result: clouds } = await api.searchClouds({
      filter: searchFilter,
      sort: getSortEntityFromSortForm(sort),
    });
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
