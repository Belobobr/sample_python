import type { Meta, StoryObj } from '@storybook/react';

import { CloudRow } from '../../components/clouds';
import { azureCloudAllFields, azureCloudRequiredFields } from './fixtures';

const meta = {
  title: 'CloudRow',
  component: CloudRow,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof CloudRow>;

export default meta;
type Story = StoryObj<typeof meta>;

export const AllFields: Story = {
  args: {
    cloud: azureCloudAllFields,
  },
};

export const RequiredFields: Story = {
  args: {
    cloud: azureCloudRequiredFields,
  },
};
