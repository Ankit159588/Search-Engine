package com.ankit.auth.security;

import com.ankit.auth.model.User;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;

public class CustomUserDetails implements UserDetails {

    // We keep the original User object inside, so we can access
    // things like id, email, role later if we need them
    private final User user;

    public CustomUserDetails(User user) {
        this.user = user;
    }

    // Lets other code (like the controller) get the original User back out
    public User getUser() {
        return user;
    }

    // Spring Security calls this to check the password during login
    @Override
    public String getPassword() {
        return user.getPassword();
    }

    // Spring Security calls this to identify the user
    @Override
    public String getUsername() {
        return user.getUsername();
    }

    // Spring Security uses this to know what the user is allowed to do
    // We convert our Role enum (e.g. "ADMIN") into the format Spring Security expects
    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        String roleName = "ROLE_" + user.getRole().name();
        GrantedAuthority authority = new SimpleGrantedAuthority(roleName);
        return List.of(authority);
    }

    // These four methods control account status.
    // We're not building account-locking/expiry features right now,
    // so we simply return true for all of them (meaning: "account is fine, allow login")
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}