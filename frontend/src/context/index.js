import { devConfig } from './dev'
import { prodConfig } from './prod'

let globalContext

if (process.env.NODE_ENV === 'production') {
    globalContext = prodConfig
} else {
    globalContext = devConfig
}

export default globalContext
