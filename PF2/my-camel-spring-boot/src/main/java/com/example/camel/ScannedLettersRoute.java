package com.example.camel;

import org.apache.camel.builder.RouteBuilder;
import org.springframework.stereotype.Component;

@Component
public class ScannedLettersRoute extends RouteBuilder {

    @Override
    public void configure() throws Exception {

        from("timer:tick?period=5000")
          .log("Camel is alive! Timer tick...");
        
        // Basic error handling (optional)
        errorHandler(defaultErrorHandler()
                        .maximumRedeliveries(3)
                        .redeliveryDelay(2000));

        // Watch the folder "data/scanned-letters" for .txt files
        from("file:data/scanned-letters?noop=true&include=.*\\.txt")
            .log("New scanned letter file: ${header.CamelFileName}")
            .process(exchange -> {
                // Read file content
                String fileContent = exchange.getIn().getBody(String.class);
                // Build JSON body for the target REST service
                String requestBody = String.format("{\"text\":\"%s\"}",
                                   fileContent.replace("\n", " "));
                exchange.getIn().setBody(requestBody);
            })
            .setHeader("Content-Type", constant("application/json"))
            // Post to XmasWishes or any REST endpoint
            .to("http://localhost:3000/wishes?httpMethod=POST")
            .log("Letter sent. Response: ${body}");
    }
}