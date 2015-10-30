(ns helloworld.integration
  (:require [helloworld.test-common :refer :all]
            [clj-http.client :as http]
            [environ.core :refer [env]]
            [midje.sweet :refer :all]))

(fact-group
 :integration

 (fact "Ping resource returns 200 HTTP response"
       (let [response (http/get (url+ "/ping")  {:throw-exceptions false})]
         response => (contains {:status 200})))

 (fact "Healthcheck resource returns 200 HTTP response"
       (let [response (http/get (url+ "/healthcheck") {:throw-exceptions false})]
         response => (contains {:status 200})))

 (fact "Hello reponds with name missing response when no name is supplied"
       (let [{status :status body :body} (http/get (url+ "/hello")
                                                   {:throw-exceptions false
                                                    :as :json})]
         status => 200
         body => {:message "What is your name?"}))

 (fact "Hello responds with Hello message when name is supplied"
       (let [{status :status body :body} (http/get (url+ "/hello")
                                                   {:throw-exceptions false
                                                    :as :json
                                                    :query-params {"name" "Bob"}})]
         status => 200
         body => {:message "Hello Bob"})))
