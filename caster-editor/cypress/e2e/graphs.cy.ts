import { aliasQuery } from '../utils';

describe('Graphs overview page', () => {
    beforeEach(() => {
        cy.intercept('POST', 'http://127.0.0.1:8081/graphql', (req) => {
            // Queries
            aliasQuery(req, 'GetGraphs')
        });
    });

    // it('login on error', () => {
    //     cy.intercept('POST', 'http://127.0.0.1:8081/graphql', (req) => {
    //         // from https://docs.cypress.io/guides/end-to-end-testing/working-with-graphql
    //         if (hasOperationName(req, 'GetGraphs')) {
    //             req.alias = 'gqlGetGraphsQuery'
    //             req.reply((res) => {
    //                 res.body.data = undefined
    //                 res.body.errors = [{ error: "error", name: "no auth" }];
    //             })
    //         }
    //     })
    //     cy.visit('/graphs');
    //     cy.contains('Please login');
    // });

    it('show uuid of graphs', () => {
        cy.intercept('POST', 'http://127.0.0.1:8081/graphql', { fixture: 'graphs.json' });
        cy.visit('/graphs');
        cy.contains("Select one of your Graphs");
        cy.contains("b611fdaf-331f-4853-b10f-f593e181f115");
    });

    it('create new graph', () => {
        cy.intercept('POST', 'http://127.0.0.1:8081/graphql', { fixture: 'graphs.json' });
        cy.visit('/graphs');
        cy.get(':last-child > .graph > div').click();
        cy.on('window:alert', (t) => {
            expect(t).to.contains('tbd');
        })
    });
})
