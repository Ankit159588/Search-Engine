package com.ankit.auth.search.service;

import com.ankit.auth.search.dto.SearchResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;


@Service
public class SearchService {
    private final RestClient restClient;

    public SearchService() {
        this.restClient = RestClient
                .builder()
                .baseUrl("http://localhost:8000")
                .build();
    }


    public SearchResponse search(String query) {

        return restClient
                .get()
                .uri(uriBuilder -> uriBuilder
                        .path("/search")
                        .queryParam("query", query)
                        .build())
                .retrieve()
                .body(SearchResponse.class);
    }

}
