// Pulled from the Square Web SDK
const APPLICATION_ID = 'sandbox-sq0idb-nmDwaVz9m2bkzGGK_dQJsg'
const LOCATION_ID = 'LXD3BVFHEVCS0'

async function main() {
  const payments = Square.payments(APPLICATION_ID, LOCATION_ID)

  const card = await payments.card()

  await card.attach('#card-container')

  async function eventHandler(event) {
    event.preventDefault()

    try {
      const result = await card.tokenize()

      if (result.status === 'OK') {
        console.log(`Payment token is ${result.token}`)
      }
    } catch (e) {
      console.error(e)
    }
  }

  const cardButton = document.getElementById('card-button')

  cardButton.addEventListener('click', eventHandler)
}

main()
