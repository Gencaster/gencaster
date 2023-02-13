import { aliasQuery } from '../utils';

describe('Landing page', () => {
  beforeEach(() => {
    cy.intercept('POST', 'http://127.0.0.1:8081/graphql', (req) => {
      // Queries
      aliasQuery(req, 'GetGraph')
    });
  });

  it('show add node button', () => {
    cy.intercept('POST', 'http://127.0.0.1:8081/graphql', {fixture: 'graph.json'});
    cy.visit('/graph/b611fdaf-331f-4853-b10f-f593e181f115');
    // cy.contains("Add node");
  });
})
