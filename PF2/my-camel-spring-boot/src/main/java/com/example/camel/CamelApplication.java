package com.example.camel;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.apache.camel.CamelContext;
import org.springframework.beans.factory.annotation.Autowired;
import jakarta.annotation.PostConstruct; // For Spring Boot 3 (Jakarta)

@SpringBootApplication
public class CamelApplication {

    @Autowired(required = false)
    CamelContext camelContext;  // from org.apache.camel

    public static void main(String[] args) {
        SpringApplication.run(CamelApplication.class, args);
    }

}
