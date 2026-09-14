#pragma once
#include "engine.hpp"
namespace rxt {
int domain_service(const std::filesystem::path& socket,const std::filesystem::path& source,const std::filesystem::path& store);
int domain_client(const std::filesystem::path& socket,const std::filesystem::path& job);
}
