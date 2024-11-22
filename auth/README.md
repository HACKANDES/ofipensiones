# Ofipensiones Auth

Ofipensiones authentication endpoint

The authentication flow is as follows:

First we have 2 resources to have in mind, 
a pair of `public` and `private` keys.

The private key will be in charge of generating `JWTs` and the public one
will decode the contents of the `JWT`.

So the deployment must place the both keys on the authentication endpoint,
and **ONLY** the public key on the services which want to use the auth server.

1. So, first the user **MUST** be registered.
2. Then the user must ask for an authentication token `JWT`
3. The user can use the authentication token to consume services until
it expires
