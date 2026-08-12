package com.ankit.auth.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.jspecify.annotations.NonNull;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;


@Component
@RequiredArgsConstructor
public class JwtAuthFilter extends OncePerRequestFilter {

    private final JwtUtils jwtUtils;
    private final CustomUserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(
            @NonNull HttpServletRequest request,
            @NonNull HttpServletResponse response,
            @NonNull FilterChain filterChain
    ) throws ServletException, IOException {
        // step 1 look for the authorization header
        String authHeader = request.getHeader("Authorization");
        // Step 2: If there's no header, or it doesn't start with "Bearer ",
        // just let the request continue — it might be hitting a public
        // endpoint like /api/auth/login, which doesn't need a token
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        // Step 3: Extract the actual token string
        // "Bearer eyJhbGciOi..." → we only want the part after "Bearer "
        String token = authHeader.substring(7);

        // Step 4: Pull the username out of the token
        String username = jwtUtils.extractUsername(token);

        // Step 5: If we got a username, and this request isn't already
        // authenticated, let's verify the token and log the user in
        // for this request
        if(username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            // Look up the full user details from the database
            UserDetails userDetails = userDetailsService.loadUserByUsername(username);

            // check validity of the token (signature, expiration, etc)
            boolean isValid = jwtUtils.validateToken(token, userDetails);

            if(isValid){
                // Build an "Authentication" object — this is what Spring
                // Security uses internally to know "who is making this request"
                UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null, //// no password needed here, token already proved identity
                        userDetails.getAuthorities()
                );
                authToken.setDetails(
                        new WebAuthenticationDetailsSource().buildDetails(request)
                );

                // Set the authentication object in the security context
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }
        // Step 6: Continue the filter chain (this is important!)
        filterChain.doFilter(request, response);
    }
}
