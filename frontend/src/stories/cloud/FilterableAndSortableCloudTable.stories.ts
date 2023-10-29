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

export const AllFields: Story = {
  args: {
    clouds: cloudsAllFields,
  },
};


