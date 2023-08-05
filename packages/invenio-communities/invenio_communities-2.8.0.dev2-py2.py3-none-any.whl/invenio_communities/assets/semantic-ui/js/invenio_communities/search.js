/*
 * This file is part of Invenio.
 * Copyright (C) 2016-2021 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React, { useState } from "react";
import {
  Input,
  Card,
  Container,
  Checkbox,
  Grid,
  Label,
  List,
  Icon,
  Item,
  Button,
  Segment,
  Accordion
} from "semantic-ui-react";
import { createSearchAppInit } from "@js/invenio_search_ui";
import {
  SearchAppFacets,
  SearchAppResultsPane,
} from "@js/invenio_search_ui/components";
import {
  BucketAggregation,
  SearchBar,
  Count,
  Sort,
  ResultsList,
  Pagination,
  ResultsPerPage,
} from "react-searchkit";
import { i18next } from "@translations/invenio_communities/i18next";
import { CommunitiesFacetsValues } from './search/components';


function ResultsGridItemTemplate({ result, index }) {
  return (
    <Card fluid key={index} href={`/communities/${result.metadata.id}`}>
      <Card.Content>
        <Card.Header>{result.metadata.title}</Card.Header>
        <Card.Description>
            <div className="truncate-lines-2"
              dangerouslySetInnerHTML={{
                __html: result.metadata.description,
              }}
            />
        </Card.Description>
      </Card.Content>
    </Card>
  );
}

function ResultsItemTemplate({ result, index }) {
  return (
    <Item key={index}>
      <Item.Content>
        <Button
          compact
          size="small"
          floated="right"
          icon
          labelPosition="left"
          href={`/communities/${result.id}`}
        >
          <Icon name="eye" />
          {i18next.t("View")}
        </Button>
        <Item.Header href={`/communities/${result.id}`}>
          {result.metadata.title}
        </Item.Header>
        <Item.Description>
            <div className="truncate-lines-2"
              dangerouslySetInnerHTML={{
                __html: result.metadata.description,
              }}
            />
        </Item.Description>
      </Item.Content>
    </Item>
  );
}

export const CommunitiesResults = ({
  sortOptions,
  paginationOptions,
  currentResultsState,
}) => {
  const { total } = currentResultsState.data;
  return (
    total && (
      <Grid>
        <Grid.Row>
          <Grid.Column width={16}>
            <Segment>
              <Grid>
                <Grid.Row
                  verticalAlign="middle"
                  className="small padding-tb-5 deposit-result-header"
                >
                  <Grid.Column width={4}>
                    <Count
                      label={() => (
                        <>
                          {i18next.t("{{total}} result(s) found", {
                            total: total,
                          })}
                        </>
                      )}
                    />
                  </Grid.Column>
                  <Grid.Column
                    width={12}
                    textAlign="right"
                    className="padding-r-5"
                  >
                    {sortOptions && (
                      <Sort
                        values={sortOptions}
                        label={(cmp) => (
                          <>
                            {i18next.t("Sort by {{cmp}}", {
                              cmp: cmp,
                            })}
                          </>
                        )}
                      />
                    )}
                  </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                  <Grid.Column>
                    <ResultsList />
                  </Grid.Column>
                </Grid.Row>
              </Grid>
            </Segment>
          </Grid.Column>
        </Grid.Row>
        <Grid.Row verticalAlign="middle">
          <Grid.Column width={4}></Grid.Column>
          <Grid.Column width={8} textAlign="center">
            <Pagination
              options={{
                size: "mini",
                showFirst: false,
                showLast: false,
              }}
            />
          </Grid.Column>
          <Grid.Column textAlign="right" width={4}>
            <ResultsPerPage
              values={paginationOptions.resultsPerPage}
              label={(cmp) => (
                <>
                  {i18next.t("{{cmp}} results per page", {
                    cmp: cmp,
                  })}
                </>
              )}
            />
          </Grid.Column>
        </Grid.Row>
      </Grid>
    )
  );
};

export const CommunitiesSearchBarElement = ({
  placeholder: passedPlaceholder,
  queryString,
  onInputChange,
  executeSearch,
}) => {
  const placeholder = passedPlaceholder || i18next.t("Search");
  const onBtnSearchClick = () => {
    executeSearch();
  };
  const onKeyPress = (event) => {
    if (event.key === "Enter") {
      executeSearch();
    }
  };
  return (
    <Input
      action={{
        icon: "search",
        onClick: onBtnSearchClick,
        className: "search",
      }}
      fluid
      placeholder={placeholder}
      onChange={(event, { value }) => {
        onInputChange(value);
      }}
      value={queryString}
      onKeyPress={onKeyPress}
    />
  );
};

const CommunitiesFacets = ({ aggs, currentResultsState }) => {
  return (
    <>
      {aggs.map((agg) => {
        return (
          <div className="facet-container" key={agg.title}>
            <BucketAggregation title={agg.title} agg={agg} />
          </div>
        );
      })}
    </>
  );
};

const RDMBucketAggregationElement = ({ title, containerCmp }) => {
  return (
    <Card className="borderless facet">
      <Card.Content>
        <Card.Header>{title}</Card.Header>
      </Card.Content>
      <Card.Content>{containerCmp}</Card.Content>
    </Card>
  );
};
export const CommunitiesSearchLayout = (props) => (
  <Container>
    <Grid>
      <Grid.Row columns={3}>
        <Grid.Column width={4} />
        <Grid.Column width={8}>
          <SearchBar placeholder={i18next.t("Search communities...")} />
        </Grid.Column>
        <Grid.Column width={4}>
          <Button
            color="green"
            icon="upload"
            labelPosition="left"
            href="/communities/new"
            content={i18next.t("New community")}
            floated="right"
          />
        </Grid.Column>
      </Grid.Row>
      <Grid.Row>
        <Grid.Column width={4}>
          <SearchAppFacets aggs={props.config.aggs} />
        </Grid.Column>
        <Grid.Column width={12}>
          <SearchAppResultsPane layoutOptions={props.config.layoutOptions} />
        </Grid.Column>
      </Grid.Row>
    </Grid>
  </Container>
);

const defaultComponents = {
  "BucketAggregation.element": RDMBucketAggregationElement,
  "BucketAggregationValues.element": CommunitiesFacetsValues,
  "SearchApp.facets": CommunitiesFacets,
  "ResultsList.item": ResultsItemTemplate,
  "ResultsGrid.item": ResultsGridItemTemplate,
  "SearchApp.layout": CommunitiesSearchLayout,
  "SearchBar.element": CommunitiesSearchBarElement,
  "SearchApp.results": CommunitiesResults,
};
const domContainer = document.getElementById("communities-search");
const facetsConfig = JSON.parse(domContainer.dataset.facetsConfig);

// Auto-initialize search app
const initSearchApp = createSearchAppInit(defaultComponents);
