export const hasOperationName = (req, operationName) => {
    const { body } = req
    return (
        // eslint-disable-next-line no-prototype-builtins
        body.hasOwnProperty('operationName') && body.operationName === operationName
    )
}


export const aliasQuery = (req, operationName) => {
    if (hasOperationName(req, operationName)) {
        req.alias = `gql${operationName}Query`
    }
}


export const aliasMutation = (req, operationName) => {
    if (hasOperationName(req, operationName)) {
        req.alias = `gql${operationName}Mutation`
    }
}


export const aliasSubscription = (req, operationName) => {
    if (hasOperationName(req, operationName)) {
        req.alias = `gql${operationName}Subscription`
    }
}
