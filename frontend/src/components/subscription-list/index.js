import styles from './styles.module.css'
import cn from 'classnames'
import { Subscription } from '../index'

const SubscriptionList = ({ subscriptions, removeSubscription }) => {
  return <div className={styles.subscriptionList}>
    {subscriptions && subscriptions.map(subscription => <Subscription
      key={subscription.id}
      removeSubscription={removeSubscription}
      {...subscription}
    />)}
  </div>
}

export default SubscriptionList
