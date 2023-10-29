import type { Meta, StoryObj } from '@storybook/react';

import { CloudFilter, FilterableAndSortableCloudTable } from '../../components/clouds';
import { cloudsAllFields } from './fixtures';
import { CloudFilter as CloudFilterEntity, CloudSort as CloudSortEntity } from '../../entities'

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
  },
};

export const All: Story = {
  args: {
    clouds: cloudsAllFields,
    filter: { provider: 'aws' },
    sort: { user_geo_latitude: 0, user_geo_longitude: 0 },
  },
};




