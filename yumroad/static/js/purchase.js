function purchase(session_id, stripe) {
    stripe.redirectToCheckout({
        sessionId: session_id
    }).then(function (result) {
        alert(result.error.message)
    });
}