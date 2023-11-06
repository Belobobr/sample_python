# backend

observability (depends on infrastracture), generaly we should monitor cache hit ratio. Not sure about our case
cache eviction policy, cache error policy
check different caching strategy (based on tiles)
clean structure for api and backend

# frontend

* ui kit wrapper (incapsulate all ui components in internal uikit, initially it could just reexport material ui kit), use ui kit like material design
* components in separate files
* styled components (better readability) => <TabPanelContainer> is bettern then <div className="tabPanelContainer">
* work correctly with forms (we could use formik or something similar)
* better types

# Common structure
sometimes we should use separate data strcutures on each level (just cumbersome)
