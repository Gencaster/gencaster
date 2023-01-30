describe("open the first graph", () => {
  beforeEach(() => {
    cy.viewport(1440, 900); // macbook pro
    cy.visit("http://127.0.0.1:8081/admin/");
    cy.get("#id_username").type("admin");
    cy.get("#id_password").type("admin");
    cy.get("form").submit();
  });

  it("Basic graph add and delete", () => {
    cy.visit("http://127.0.0.1:3001/graphs/");
    cy.get(".graph-selection").first().click();
    cy.wait(500);
    cy.get(".add-node-btn").click();
    cy.wait(500);
    cy.get(".v-network-graph").click(720, 420);
    cy.get(".remove-btn").click();
    cy.get(".dialog-delete-node-btn").click();
    cy.wait(1000);
  });

  it("Basic graph add and delete", () => {
    cy.visit("http://127.0.0.1:3001/graphs/");
    cy.get(".graph-selection").first().click();
    cy.wait(500);
    cy.get(".add-node-btn").click();
    cy.wait(500);
    cy.get(".v-network-graph").click(720, 420);
    cy.get(".v-network-graph").click(720, 420);
    // cy.get(".v-network-graph").dblclick(720, 420);
    cy.wait(15000);
  });

  // it("Pick first Graph", () => {
  //   cy.visit("http://127.0.0.1:3001/graphs/");
  // });
});
