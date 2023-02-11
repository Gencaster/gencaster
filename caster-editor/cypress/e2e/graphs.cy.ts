import { aliasMutation, aliasQuery, hasOperationName } from '../utils';

describe('Graphs overview page', () => {
    beforeEach(() => {
        cy.intercept('POST', 'http://127.0.0.1:8081/graphql', (req) => {
            // Queries
            aliasQuery(req, 'GetGraphs');
            aliasMutation(req, 'CreateGraph');
        });
    });

    it('show uuid of graphs', () => {
        cy.intercept('POST', 'http://127.0.0.1:8081/graphql', { fixture: 'graphs.json' });
        cy.visit('/graphs');
        cy.contains("Select one of your Graphs");
        cy.contains("b611fdaf-331f-4853-b10f-f593e181f115");
    });

    it('mock create new graph', () => {
        cy.intercept('POST', 'http://127.0.0.1:8081/graphql', (req) => {
            if (hasOperationName(req, 'GetGraphs')) {
                req.reply({fixture: "graphs.json"});
            }
            if (hasOperationName(req, 'CreateGraph')) {
                req.alias = 'gqlCreateGraphMutation';
                req.reply({fixture: "createGraph.json"});
            }

        });
        cy.visit('/graphs');
        cy.get(':last-child > .graph > div').click();
        cy.get('#graphNameInput').type("my_test_graph");
        cy.get('.el-button--primary > span').click();
        cy.wait('@gqlCreateGraphMutation');
        cy.wait(1000);
        cy.get('#graphNameInput').should('not.visible', {timeout: 10000});
    });

    it('error when creating same named graph', () => {
        cy.intercept('POST', 'http://127.0.0.1:8081/graphql', (req) => {
            if (hasOperationName(req, 'GetGraphs')) {
                req.reply({fixture: "graphs.json"});
            }
            if (hasOperationName(req, 'CreateGraph')) {
                req.alias = 'gqlCreateGraphMutation';
                req.reply({fixture: "createGraphSameError.json"});
            }
        });
        cy.visit('/graphs');
        cy.get(':last-child > .graph > div').click();
        cy.get('#graphNameInput').type("my_test_graph");
        cy.get('.el-button--primary > span').click();
        cy.wait('@gqlCreateGraphMutation');
        cy.wait(1000);
        cy.get('#graphNameInput').should('be.visible', {timeout: 10000});
        cy.on('window:alert', (t) => {
            expect(t).to.contains('Could not create graph');
        })
    });
})
