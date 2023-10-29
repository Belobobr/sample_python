import type { Meta, StoryObj } from '@storybook/react';

import { CloudRow } from '../../components/clouds';
import { azureCloudAllFields, azureCloudRequiredFields } from './fixtures';

const meta = {
  title: 'CloudRow',
  component: CloudRow,
  parameters: {
    // Optional parameter to center the component in the Canvas. More info: https://storybook.js.org/docs/react/configure/story-layout
    layout: 'centered',
  },
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ['autodocs'],
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
  //   argTypes: {
  //     backgroundColor: { control: 'color' },
  //   },
} satisfies Meta<typeof CloudRow>;

export default meta;
type Story = StoryObj<typeof meta>;

// More on writing stories with args: https://storybook.js.org/docs/react/writing-stories/args
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
