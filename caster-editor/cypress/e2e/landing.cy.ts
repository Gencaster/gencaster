import { aliasQuery, hasOperationName } from '../utils';

describe('Landing page', () => {
    beforeEach(() => {
        cy.intercept('POST', 'http://127.0.0.1:8081/graphql', (req) => {
            // Queries
            aliasQuery(req, 'GetGraphs')
        });
    });

    it('login on error', () => {
        cy.intercept('POST', 'http://127.0.0.1:8081/graphql', (req) => {
            // from https://docs.cypress.io/guides/end-to-end-testing/working-with-graphql
            if (hasOperationName(req, 'GetGraphs')) {
                req.alias = 'gqlGetGraphsQuery'
                req.reply((res) => {
                    res.body.data = undefined
                    res.body.errors = [{ error: "error", name: "no auth" }];
                })
            }
        })
        cy.visit('/');
        cy.contains('GenCaster');
        cy.get('.login-button').contains("Login");
    });

    it('redirect to graphs', () => {
        cy.intercept('POST', 'http://127.0.0.1:8081/graphql', { fixture: 'graphs.json' });
        cy.visit('/');
        cy.contains("Select one of your Graphs");
    });
})
