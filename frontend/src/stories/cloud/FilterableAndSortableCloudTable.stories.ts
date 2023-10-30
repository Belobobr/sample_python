import type { Meta, StoryObj } from '@storybook/react';

import { FilterableAndSortableCloudTable } from '../../components/clouds';
import { cloudsAllFields } from './fixtures';

const meta = {
  title: 'FilterableAndSortableCloudTable',
  component: FilterableAndSortableCloudTable,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof FilterableAndSortableCloudTable>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    clouds: cloudsAllFields,
    filter: {},
    sort: {},
    loading: false,
    errors: {},
  },
};

export const All: Story = {
  args: {
    clouds: cloudsAllFields,
    filter: { provider: 'aws' },
    sort: { user_geo_latitude: 0, user_geo_longitude: 0 },
    loading: false,
    errors: {},
  },
};

export const ContentLoading: Story = {
  args: {
    clouds: cloudsAllFields,
    filter: { provider: 'aws' },
    sort: { user_geo_latitude: 0, user_geo_longitude: 0 },
    loading: true,
    errors: {},
  },
};

export const ContentError: Story = {
  args: {
    clouds: cloudsAllFields,
    filter: { provider: 'aws' },
    sort: { user_geo_latitude: 0, user_geo_longitude: 0 },
    loading: false,
    errors: {
      serverErrors: [
        {
          status: 0,
          message: 'Error message',
          more_info: 'More info',
        },
      ],
    },
  },
};
