import type { Meta, StoryObj } from '@storybook/react';

import { Errors } from '../../components/clouds';

const meta = {
  title: 'Errors',
  component: Errors,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof Errors>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    errors: {},
  },
};

export const NoErrors: Story = {
  args: {
    errors: {},
  },
};

export const ServerErrors: Story = {
  args: {
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

export const StatusError: Story = {
  args: {
    errors: {
      statusError: 412,
    },
  },
};

export const ClientError: Story = {
  args: {
    errors: {
      clientError: 'Client error',
    },
  },
};
