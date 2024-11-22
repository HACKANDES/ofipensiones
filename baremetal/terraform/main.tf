terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_compute_network" "ofipensiones_network" {
  name                    = "ofipensiones-network"
  auto_create_subnetworks = true
}

resource "google_compute_firewall" "allow_http" {
  name    = "allow-http"
  network = google_compute_network.ofipensiones_network.name

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }

  direction = "INGRESS"

  source_ranges = ["0.0.0.0/0"]

  target_tags = ["http"]
}

resource "google_compute_firewall" "allow_ssh" {
  name = "allow-ssh"

  allow {
    ports    = ["22"]
    protocol = "tcp"
  }

  direction     = "INGRESS"
  network       = google_compute_network.ofipensiones_network.id
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}

resource "google_compute_address" "auth_server_public_ip" {
  name         = "auth-server-public-ip"
  address_type = "EXTERNAL"
  network_tier = "PREMIUM"
}

resource "google_compute_instance" "auth_server" {
  name         = "auth-i"
  machine_type = var.auth_server_vm
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.auth_server_image
    }
  }

  network_interface {
    network = google_compute_network.ofipensiones_network.name
    access_config {
      nat_ip = google_compute_address.auth_server_public_ip.address
    }
  }

  scheduling {
    preemptible = true
    automatic_restart  = false
    provisioning_model = "SPOT"
    max_run_duration {
      seconds = 3600
    }
  }

  metadata = {
    user-data = file("cloud-config.yml")
  }

  tags = ["http", "ssh"]
}

output "auth_server_private_ip" {
  value = google_compute_instance.auth_server.network_interface.0.network_ip
}

output "auth_server_public_ip" {
  value = google_compute_instance.auth_server.network_interface.0.access_config.0.nat_ip
}