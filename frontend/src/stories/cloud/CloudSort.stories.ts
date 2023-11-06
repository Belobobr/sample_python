import type { Meta, StoryObj } from '@storybook/react';

import { CloudSort } from '../../components/clouds';

const meta = {
  title: 'CloudSort',
  component: CloudSort,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof CloudSort>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    sort: { user_geo_latitude: undefined, user_geo_longitude: undefined },
  },
};
