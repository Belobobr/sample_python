import type { Meta, StoryObj } from '@storybook/react';

import { CloudFilter } from '../../components/clouds';

const meta = {
  title: 'CloudFilter',
  component: CloudFilter,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof CloudFilter>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    
  },
};


