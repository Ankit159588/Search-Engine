package com.ankit.auth;

import io.github.cdimascio.dotenv.Dotenv;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@SpringBootApplication
public class AuthApplication {

    public static void main(String[] args) {
        Dotenv dotenv = Dotenv.configure()
                .ignoreIfMissing()
                .load();

        dotenv.entries().forEach(entry ->
                System.setProperty(entry.getKey(), entry.getValue())
        );
//        System.out.println("DB URL: " + System.getProperty("DB_URL"));
//        System.out.println("DB_USERNAME: " + System.getProperty("DB_USERNAME"));
//        System.out.println("DB_PASSWORD length: " + System.getProperty("DB_PASSWORD").length());
        SpringApplication.run(AuthApplication.class, args);
    }
}

