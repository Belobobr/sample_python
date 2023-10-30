import type { Meta, StoryObj } from '@storybook/react';
import { userEvent, waitFor, within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';

import { FilterableAndSortableCloudTableContainer } from '../../components/clouds';
import { cloudsAllFields } from './fixtures';

const meta = {
  title: 'FilterableAndSortableCloudTableContainer',
  component: FilterableAndSortableCloudTableContainer,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof FilterableAndSortableCloudTableContainer>;

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

// TODO check how to reuse steps
export const SearchSuccess: Story = {
  play: async ({ args, canvasElement, step }) => {
    const canvas = within(canvasElement);

    await step('Enter filter', async () => {
      await userEvent.type(canvas.getByTestId('filterProviderInput'), 'aws');
    });

    await step('Enter sort', async () => {
      await userEvent.type(canvas.getByTestId('sortUserGeoLatitudeInput'), '15');
      await userEvent.type(canvas.getByTestId('sortUserGeoLongitudeInput'), '8');
    });

    await step('Search', async () => {
      await userEvent.click(canvas.getByTestId('searchButton'));
      await waitFor(() => expect(canvas.getByTestId('searchLoader')).toBeInTheDocument());
    });

    await waitFor(() => expect(canvas.getByTestId('searchContent')).toBeInTheDocument());
  },
};

export const SearchFailure: Story = {
  play: async ({ args, canvasElement, step }) => {
    const canvas = within(canvasElement);

    await step('Enter filter', async () => {
      await userEvent.type(canvas.getByTestId('filterProviderInput'), 'aws');
    });

    await step('Enter sort', async () => {
      await userEvent.type(canvas.getByTestId('sortUserGeoLatitudeInput'), '15');
      await userEvent.type(canvas.getByTestId('sortUserGeoLongitudeInput'), '8');
    });

    await step('Search', async () => {
      await userEvent.click(canvas.getByTestId('searchButton'));
      await waitFor(() => expect(canvas.getByTestId('searchLoader')).toBeInTheDocument());
    });

    await waitFor(() => expect(canvas.getByTestId('searchError')).toBeInTheDocument());
  },
};
