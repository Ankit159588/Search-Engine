package com.ankit.auth.service;

import com.ankit.auth.dto.AuthResponse;
import com.ankit.auth.dto.LoginRequest;
import com.ankit.auth.dto.RegisterRequest;
import com.ankit.auth.exception.UserAlreadyExistsException;
import com.ankit.auth.model.Role;
import com.ankit.auth.model.User;
import com.ankit.auth.repository.UserRepository;
import com.ankit.auth.security.CustomUserDetails;
import com.ankit.auth.security.JwtUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtils jwtUtils;
    private final AuthenticationManager authenticationManager;

    public AuthResponse register(RegisterRequest request) {

        // Step 1: Check if username or email is already taken
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new UserAlreadyExistsException("Username is already taken");
        }
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new UserAlreadyExistsException("Email is already registered");
        }

        // Step 2: Hash the password before saving
        String hashedPassword = passwordEncoder.encode(request.getPassword());

        // Step 3: Build and save the new user
        User newUser = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .password(hashedPassword)
                .role(Role.USER)
                .build();

        User savedUser = userRepository.save(newUser);

        // Step 4: Generate a token and build the response
        CustomUserDetails userDetails = new CustomUserDetails(savedUser);
        String token = jwtUtils.generateToken(userDetails);

        return buildAuthResponse(token, savedUser);
    }

    public AuthResponse login(LoginRequest request) {

        // Step 1: Verify username + password via Spring Security
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getUsername(),
                        request.getPassword()
                )
        );

        // Step 2: Get the verified user back out
        CustomUserDetails userDetails = (CustomUserDetails) authentication.getPrincipal();
        User user = userDetails.getUser();

        // Step 3: Generate a token and build the response
        String token = jwtUtils.generateToken(userDetails);

        return buildAuthResponse(token, user);
    }

    // Small private helper — avoids repeating the same response-building
    // code in both register() and login()
    private AuthResponse buildAuthResponse(String token, User user) {
        return AuthResponse.builder()
                .token(token)
                .username(user.getUsername())
                .email(user.getEmail())
                .role(user.getRole().name())
                .build();
    }
}