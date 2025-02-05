import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product.model';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-product-form',
  templateUrl: './product-form.component.html',
  styleUrls: ['./product-form.component.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class ProductFormComponent implements OnInit {
  productForm: FormGroup;
  isEditMode = false;
  productId?: number;

  constructor(
    private fb: FormBuilder,
    private productService: ProductService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.productForm = this.fb.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
      price: ['', [Validators.required, Validators.min(0)]],
      imageUrl: ['']
    });
  }

  ngOnInit(): void {
    this.productId = Number(this.route.snapshot.paramMap.get('id'));
    if (this.productId) {
      this.isEditMode = true;
      this.loadProduct(this.productId);
    }
  }

  loadProduct(id: number): void {
    this.productService.getProductById(id).subscribe({
      next: (product) => {
        this.productForm.patchValue(product);
      },
      error: (error) => {
        console.error('Erreur lors du chargement du produit:', error);
      }
    });
  }

  onSubmit(): void {
    if (this.productForm.valid) {
      const product: Product = this.productForm.value;
      
      if (this.isEditMode && this.productId) {
        this.productService.updateProduct(this.productId, product).subscribe({
          next: () => {
            this.router.navigate(['/products']);
          },
          error: (error) => {
            console.error('Erreur lors de la mise à jour:', error);
          }
        });
      } else {
        this.productService.createProduct(product).subscribe({
          next: () => {
            this.router.navigate(['/products']);
          },
          error: (error) => {
            console.error('Erreur lors de la création:', error);
          }
        });
      }
    }
  }
} 