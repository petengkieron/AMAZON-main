import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { CommonModule } from '@angular/common';
import { Product } from '../../models/product.model';

@Component({
  selector: 'app-product-form',
  templateUrl: './product-form.component.html',
  styleUrls: ['./product-form.component.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class ProductFormComponent implements OnInit {
  productForm: FormGroup;
  error: string | null = null;
  isEditMode: boolean = false;
  productId: number | null = null;

  constructor(
    private fb: FormBuilder,
    private productService: ProductService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.productForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      description: ['', [Validators.required, Validators.minLength(10)]],
      price: ['', [Validators.required, Validators.min(0)]],
      category: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      if (params['id']) {
        this.isEditMode = true;
        this.productId = +params['id'];
        this.loadProduct(this.productId);
      }
    });
  }

  loadProduct(id: number): void {
    this.productService.getProductById(id).subscribe({
      next: (product) => {
        this.productForm.patchValue(product);
      },
      error: (error) => {
        console.error('Error loading product:', error);
        this.error = 'Failed to load product details.';
      }
    });
  }

  onSubmit(): void {
    if (this.productForm.valid) {
      const productData: Product = this.productForm.value;
      console.log('Submitting form with data:', productData);
      
      const operation = this.isEditMode
        ? this.productService.updateProduct(this.productId!, productData)
        : this.productService.createProduct(productData);

      operation.subscribe({
        next: (response) => {
          console.log('Product operation successful:', response);
          this.router.navigate(['/products']);
        },
        error: (error) => {
          console.error('Error during product operation:', error);
          this.error = error.message || 'An error occurred. Please try again.';
        }
      });
    } else {
      console.log('Form is invalid:', this.productForm.errors);
      this.error = 'Please fill out all required fields correctly.';
    }
  }

  onCancel(): void {
    this.router.navigate(['/products']);
  }
}
