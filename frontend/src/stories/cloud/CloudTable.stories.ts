import type { Meta, StoryObj } from '@storybook/react';

import { CloudsTable } from '../../components/clouds';
import { cloudsAllFields, cloudRequiredFields } from './fixtures';

const meta = {
  title: 'CloudsTable',
  component: CloudsTable,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof CloudsTable>;

export default meta;
type Story = StoryObj<typeof meta>;

export const AllFields: Story = {
  args: {
    clouds: cloudsAllFields,
  },
};


export const RequiredFields: Story = {
  args: {
    clouds: cloudRequiredFields,
  },
};


