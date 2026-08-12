package com.ankit.auth.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.function.Function;

@Component
public class JwtUtils {
    @Value("${jwt.secret}")
    private String secret;

    @Value("${jwt.expiration-ms}")
    private long expirationMs;

    private SecretKey getSigningKey() {
        byte[] secretBytes = secret.getBytes();
        return Keys.hmacShaKeyFor(secretBytes);
    }

    // Called after a successful login or register.
    // Takes the logged-in user's details and builds a signed token string
    public String generateToken(UserDetails userDetails) {
        String username = userDetails.getUsername();
        Date now = new Date();
        Date expiration = new Date(now.getTime() + expirationMs);

        SecretKey key = getSigningKey();

        return Jwts.builder()
                .subject(username)
                .issuedAt(now)
                .expiration(expiration)
                .signWith(key)
                .compact();
    }

    // ==========================================
    // READING A TOKEN
    // ==========================================

    // Opens up a token and gives back all the data stored inside it.
    // "Claims" is just the name for that bundle of data (username, dates, etc).
    private Claims extractAllClaims(String token) {
        SecretKey secretKey = getSigningKey();
        return  Jwts.parser()
                .verifyWith(secretKey)
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    // get the username from the token
    public String extractUsername(String token) {
        Claims claims = extractAllClaims(token);
        String username = claims.getSubject();
        return username; // return the username from the token

    }

        //get expiration date from the token
        public Date getExpirationDateFromToken(String token) {
            Claims claims = extractAllClaims(token);
            Date expiration = claims.getExpiration();
            return expiration;
        }

    // Gets just the expiration date out of a token
    public Date extractExpirationDate(String token) {
        Claims claims = extractAllClaims(token);
        Date expirationDate = claims.getExpiration();
        return expirationDate;
    }

    // ==========================================
    // VALIDATING A TOKEN
    // ==========================================
    // Checks if a token's expiration date is already in the past
    public boolean isTokenExpired(String token) {
        Date expirationDate = extractExpirationDate(token);
        Date now = new Date();
        return expirationDate.before(now);
    }

    public boolean validateToken(String token, UserDetails userDetails) {

        String usernameInToken = extractUsername(token);
        String actualUsername = userDetails.getUsername();

        boolean usernameMatches = usernameInToken.equals(actualUsername);
        boolean notExpired = !isTokenExpired(token);

        return usernameMatches && notExpired;
    }


}

