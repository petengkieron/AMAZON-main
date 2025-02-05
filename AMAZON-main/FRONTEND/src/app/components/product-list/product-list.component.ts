import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product.model';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent implements OnInit {
  products: Product[] = [];
  error: string | null = null;

  constructor(private productService: ProductService) {}

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.productService.getAllProducts().subscribe(
      (data) => {
        this.products = data;
      },
      (error) => {
        this.error = 'Erreur lors du chargement des produits';
        console.error('Erreur lors du chargement des produits', error);
      }
    );
  }

  deleteProduct(id: number): void {
    this.productService.deleteProduct(id).subscribe(
      () => {
        this.products = this.products.filter(product => product.id !== id);
      },
      (error) => {
        this.error = 'Erreur lors de la suppression du produit';
        console.error('Erreur lors de la suppression du produit', error);
      }
    );
  }
}
