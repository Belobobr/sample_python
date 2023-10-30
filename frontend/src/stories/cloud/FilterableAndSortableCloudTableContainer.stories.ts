import { rest } from 'msw';
import type { Meta, StoryObj } from '@storybook/react';
import { userEvent, waitFor, within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';
import { FilterableAndSortableCloudTableContainer } from '../../components/clouds';
import { cloudsAllFields } from './fixtures';
import { SearchCloudsResponseBody } from '../../api/clouds';
import { ResponseBodyError } from '../../api/server';

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

// TODO check how to reuse
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

    await step('Content shown', async () => {
      await waitFor(() => expect(canvas.getByTestId('searchContent')).toBeInTheDocument());
    });
  },
};

const successSearchResponse = new SearchCloudsResponseBody(cloudsAllFields, undefined, undefined);

SearchSuccess.parameters = {
  msw: {
    handlers: [
      rest.post('http://localhost:8080/api/clouds:search', (req, res, ctx) => {
        return res(ctx.json(successSearchResponse));
      }),
    ],
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

const errorSearchResponse = new SearchCloudsResponseBody(
  [],
  [new ResponseBodyError('Precondition failed', 412)],
  undefined,
);

SearchFailure.parameters = {
  msw: {
    handlers: [
      rest.post('http://localhost:8080/api/clouds:search', (req, res, ctx) => {
        return res(ctx.status(412), ctx.json(errorSearchResponse));
      }),
    ],
  },
};
