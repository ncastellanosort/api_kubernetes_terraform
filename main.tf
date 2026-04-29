provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment_v1" "app" {
  metadata {
    name = "motor-inferencia"
    labels = {
      app = "motor"
    }
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "motor"
      }
    }

    template {
      metadata {
        labels = {
          app = "motor"
        }
      }

      spec {
        container {
          name  = "api"
          image = "motor-inferencia:v1"

          port {
            container_port = 8000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app" {
  metadata {
    name = "motor-service"
  }

  spec {
    selector = {
      app = "motor"
    }

    port {
      port        = 80
      target_port = 8000
      node_port   = 30080
    }

    type = "NodePort"
  }
}