package com.ankit.auth.security;

import com.ankit.auth.model.User;
import com.ankit.auth.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CustomUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    // Spring Security calls this method automatically whenever it needs
    // to check a username during login, or rebuild user info from a token.
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // Step 1: try to find the user in the database
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found with username: " + username));
        // Step 2: wrap it in our translator class
        UserDetails userDetails = new CustomUserDetails(user);
        // step 3: hand it back to Spring Security
        return userDetails;
    }
}
